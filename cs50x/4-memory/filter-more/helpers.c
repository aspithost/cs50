#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "helpers.h"

void blur_pixel(int row, int col, int height, int width, RGBTRIPLE image[height][width], RGBTRIPLE new_image[height][width]);
uint8_t calc_average(uint16_t total, uint8_t n);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            uint8_t *red = &image[i][j].rgbtRed;
            uint8_t *green = &image[i][j].rgbtGreen;
            uint8_t *blue = &image[i][j].rgbtBlue;

            uint16_t sum = *red + *green + *blue;
            int average = (sum + 1) / 3;

            *red = average;
            *green = average;
            *blue = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0, n = width / 2; j < n; j++)
        {
            RGBTRIPLE tmp = image[i][width - j - 1];
            image[i][width - j - 1] = image[i][j];
            image[i][j] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE(*buffer)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    if (buffer == NULL)
    {
        printf("Could not create buffer\n");
        return;
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            blur_pixel(i, j, height, width, image, buffer);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = buffer[i][j];
        }
    }
    free(buffer);
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE(*new_image)[width] = calloc(height, width * sizeof(RGBTRIPLE));

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int16_t gx_red = 0;
            int16_t gx_green = 0;
            int16_t gx_blue = 0;
            int16_t gy_red = 0;
            int16_t gy_green = 0;
            int16_t gy_blue = 0;

            for (int k = -1; k <= 1; k++)
            {
                if (i + k < 0 || i + k >= height)
                {
                    continue;
                }
                for (int l = -1; l <= 1; l++)
                {
                    if (j + l < 0 || j + l >= width)
                    {
                        continue;
                    }
                    RGBTRIPLE pixel = image[i + k][j + l];

                    gx_red += pixel.rgbtRed * l * (k == 0 ? 2 : 1);
                    gx_green += pixel.rgbtGreen * l * (k == 0 ? 2 : 1);
                    gx_blue += pixel.rgbtBlue * l * (k == 0 ? 2 : 1);

                    gy_red += pixel.rgbtRed * k * (l == 0 ? 2 : 1);
                    gy_green += pixel.rgbtGreen * k * (l == 0 ? 2 : 1);
                    gy_blue += pixel.rgbtBlue * k * (l == 0 ? 2 : 1);
                }
            }

            int sobel_red = round(sqrt(pow(gx_red, 2) + pow(gy_red, 2)));
            int sobel_green = round(sqrt(pow(gx_green, 2) + pow(gy_green, 2)));
            int sobel_blue = round(sqrt(pow(gx_blue, 2) + pow(gy_blue, 2)));

            new_image[i][j].rgbtRed = (sobel_red > 255) ? 255 : sobel_red;
            new_image[i][j].rgbtGreen = (sobel_green > 255) ? 255 : sobel_green;
            new_image[i][j].rgbtBlue = (sobel_blue > 255) ? 255 : sobel_blue;
        }
    }

    for (int i = 0; i < height; i ++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = new_image[i][j].rgbtRed;
            image[i][j].rgbtGreen = new_image[i][j].rgbtGreen;
            image[i][j].rgbtBlue = new_image[i][j].rgbtBlue;
        }
    }
    free(new_image);
    return;
}

void blur_pixel(int row, int col, int height, int width, RGBTRIPLE image[height][width], RGBTRIPLE new_image[height][width])
{
    uint16_t total_red = 0;
    uint16_t total_green = 0;
    uint16_t total_blue = 0;
    uint8_t number_of_pixels = 0;

    for (int k = -1; k <= 1; k++)
    {
        if ((row + k) < 0 || (row + k) >= height)
        {
            continue;
        }
        for (int l = -1; l <= 1; l++)
        {
            if ((col + l) < 0 || (col + l) >= width)
            {
                continue;
            }
            RGBTRIPLE pixel = image[row + k][col + l];
            total_red += pixel.rgbtRed;
            total_green += pixel.rgbtGreen;
            total_blue += pixel.rgbtBlue;
            number_of_pixels += 1;
        }
    }
    new_image[row][col].rgbtRed = calc_average(total_red, number_of_pixels);
    new_image[row][col].rgbtGreen = calc_average(total_green, number_of_pixels);
    new_image[row][col].rgbtBlue = calc_average(total_blue, number_of_pixels);

}

uint8_t calc_average(uint16_t total, uint8_t n)
{
    if (!n)
    {
        return 0;
    }
    // printf("total: %u, n: %u, average: %u\n", total, n, (total + (n / 2)) / n);
    uint16_t average = (total + (n / 2)) / n;
    return average;
}