import torch
from torch import nn
import torch.nn.functional as F
from utils.nn_utils import get_conv_output_size, get_max_pool_output_size


class LiteFace100(nn.Module):
    def __init__(self, in_channels: int, image_size: tuple, c1: int = 16, c2: int = 32, c3: int = 64, c4: int = 128, f1: int = 512, f2: int = 128):
        super().__init__()

        # expected image channels
        self.in_channels = in_channels

        # expected height & width
        self.input_height = image_size[0]
        self.input_width = image_size[1]

        # layers config
        # out channels, kernel_size, stride, padding
        max_pool_ = ("max_pool", 2, 2, 0)
        avg_pool_ = ("avg_pool", 6, 1, 0)
        adaptive_avg_pool_ = ("adaptive_avg_pool", (6, 6))
        self.conv_layers = (
            ("conv", c1, 3, 2, 3),
            max_pool_,
            ("conv", c2, 3, 1, 1),
            max_pool_,
            ("conv", c3, 3, 1, 1),
            max_pool_,
            ("conv", c4, 3, 1, 1),
            adaptive_avg_pool_,
            avg_pool_
        )

        self.fc_layers = (
            ("linear", f1),
            # ("dropout", 0.5),
            ("leaky_relu", 0.1),
            ("linear", f2)
        )

        self.layers = []
        in_channels = self.in_channels
        input_size = (self.input_height, self.input_width)
        flatten_input = self.input_height * self.input_width * self.in_channels
        for i, layer in enumerate(self.conv_layers):
            if layer[0] == "conv":
                self.layers.append(nn.Conv2d(in_channels, layer[1], layer[2], layer[3], layer[4]))
                self.layers.append(nn.BatchNorm2d(layer[1]))
                self.layers.append(nn.LeakyReLU(0.1))
                # self.layers.append(nn.PReLU(layer[1]))
                in_channels = layer[1]
                flatten_input, input_size = get_conv_output_size(layer[1], input_size, layer[2], layer[3], layer[4])

            elif layer[0] == "max_pool":
                self.layers.append(nn.MaxPool2d(layer[1], layer[2], layer[3]))
                flatten_input, input_size = get_max_pool_output_size(in_channels, input_size, layer[1], layer[2], layer[3])

            elif layer[0] == "avg_pool":
                self.layers.append(nn.AvgPool2d(layer[1], layer[2], layer[3]))
                flatten_input, input_size = get_max_pool_output_size(in_channels, input_size, layer[1], layer[2], layer[3])

            elif layer[0] == "adaptive_avg_pool":
                self.layers.append(nn.AdaptiveAvgPool2d(layer[1]))
                flatten_input, input_size = in_channels * layer[1][0] * layer[1][1], layer[1]

        self.layers.append(nn.Flatten())
        input_len = flatten_input
        for i, layer in enumerate(self.fc_layers):
            if layer[0] == "linear":
                self.layers.append(nn.Linear(input_len, layer[1]))
                input_len = layer[1]

            elif layer[0] == "dropout":
                self.layers.append(nn.Dropout(layer[1]))

            elif layer[0] == "leaky_relu":
                self.layers.append(nn.LeakyReLU(layer[1]))

        self.sequential = nn.Sequential(*self.layers)

    @property
    def name(self):
        return f'{tuple([*self.conv_layers] + [*self.fc_layers])}'

    def forward(self, x):
        x = self.sequential(x)
        return F.normalize(x)
