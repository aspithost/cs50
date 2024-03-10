## Traffic
### Experimentation
For starters, I created the following model:
- Convolutional layer with 32 layers with a "relu" activation function
- Max Pooling layer with a pool size of (2,2)
- Convolutional layer with 32 layers
- Max Pooling layer with a pool size of (2,2)
- Flattening layer
- Dense output layer with 43 nodes and a softmax activation function.

I quickly found that this setup was not especially performant, and although the model did have an accuracy of .90-.95, it also had a high loss of .3-.4.

I then added a dense hidden layer with 128 nodes in between the flattening and output layer. This resulted in sligtly improved accuracy (~.95), but only brought down the loss to about ~.25.

I then started experimenting with adding a dropout layer of .25 after the hidden layer. This improved accuracy to about .96-.97, and significantly reduced loss to about ~.15.

Since I still found this loss value on the high end, I started experimenting with multiple convolutional layers prior to any max pooling layer. To keep performance in mind, I decided to use fewer layers per convolutional layer at the start of the model. I started using the following model:
- Convolutional layer with 8 layers with a "relu" activation function
- Convolutional layer with 8 layers with a "relu" activation function
- Max Pooling layer with a pool size of (2,2)
- Convolutional layer with 32 layers with a "relu" activation function
- Convolutional layer with 32 layers with a "relu" activation function
- Max Pooling layer with a pool size of (2,2)
- Flattening layer
- Dense hidden layer with 128 nodes
- A dropout layer with a value of .25
- Dense output layer with 43 nodes and a softmax activation function.

This model improved performance by about ~20%, significantly reduced loss to .08-.09, and improved accuracy to about ~.98.

Chaining convolutional layers seemed to work very well for these images, so I proceeded with that approach. 

To prevent further overfitting, I added a second dropout layer prior to the flattening layer with a value of .25, and increased the value of the dropout layer after the hidden layer to .4 to reduce overfitting even further. This reduced loss to about ~.07, while accuracy remained near ~.98.

Instead of two pooling layers, I now wanted to experiment with chaining many convolutional layers. As image size reduces every convolutional layer, it would become impossible to add two pooling layers.

I experimented with the following: 
- Convolutional layer with 8 layers with a "relu" activation function
- Convolutional layer with 8 layers with a "relu" activation function
- Convolutional layer with 8 layers with a "relu" activation function
- Convolutional layer with 8 layers with a "relu" activation function
- Convolutional layer with 8 layers with a "relu" activation function
- Max Pooling layer with a pool size of (2,2)
- Convolutional layer with 16 layers with a "relu" activation function
- A dropout layer with a value of .25
- Flattening layer
- Dense hidden layer with 128 nodes
- A dropout layer with a value of .4
- Dense output layer with 43 nodes and a softmax activation function.

This yielded comparable results to the previous approach, in both performance and loss/accuracy. I decided to increase the layers of the last few convolutional layers, and started to finalize my model.
### Model and its results
For my final model, I built on the approach of chaining several convolutional layers, where I increase the number of layers in the later convolutional layers. My model looks like the following:
- Convolutional layer with 8 layers with a "relu" activation function
- Convolutional layer with 8 layers with a "relu" activation function
- Convolutional layer with 8 layers with a "relu" activation function
- Convolutional layer with 16 layers with a "relu" activation function
- Convolutional layer with 32 layers with a "relu" activation function
- Max Pooling layer with a pool size of (2,2)
- Convolutional layer with 64 layers with a "relu" activation function
- A dropout layer with a value of .25
- Flattening layer
- Dense hidden layer with 128 nodes
- A dropout layer with a value of .4
- Dense output layer with 43 nodes and a softmax activation function.

This slightly worsened performance (~10-20%) compared to the previously mentioned model, but did bring down the loss significantly. The accuracy improved to about ~.985-.99, and the loss dropped to ~.04-.06.

All in all, for this exercise I found that chaining convolutional layers appears to be a good approach. Adding dropout layers significantly prevented overfitting, and reduced loss. While I also experimented with chaining several Dense hidden layers, this did not appear to provide any added value in my tests.

I was surprised to see that this model can predict any of 43 different sign types with a success percentage of 98.5-99%. 