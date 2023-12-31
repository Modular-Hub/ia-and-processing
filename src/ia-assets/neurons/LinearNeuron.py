import numpy as np
import matplotlib.pyplot as plt

## Linear Neuron
class LinearNeuron:
    def __init__(self, n_inputs, learning_rate=0.1 ) -> None:
        self.w = -1 + 2 * np.random.rand(n_inputs)
        self.b = -1 + 2 * np.random.rand()
        self.eta = learning_rate

    def predict(self, X):
        Y_est = np.dot(self.w, X) + self.b
        return Y_est

    ## Generator function to get a batch
    def batcher(self, X, Y, batch_size):
        p = X.shape[1]
        li, lu = 0, batch_size

        while True:
            if li < p:
                yield X[:, li:lu], Y[:, li:lu]
                li, lu = li + batch_size, lu + batch_size
            else:
                return None

    ## Medium Square Error
    def MSE(self, X, Y):
        p = X.shape[1]
        Y_est = self.predict(X)
        return (1/(2*p))*np.sum((Y-Y_est)**2)
    
    def fit(self, X, Y, solver='BGD', epochs=500, batch_size=20):
        error_history = []
        p = X.shape[1]

        # Stochastic Gradient Descent
        if solver == 'SGD':
            for _ in range(epochs):
                for i in range(p):
                    y_est = self.predict(X[:, i])
                    self.w += self.eta * (Y[:, i] - y_est) * X[:, i]
                    self.b += self.eta * (Y[:, i] - y_est)
            
                error_history.append(self.MSE(X, Y))

        # Batch Gradient Descent
        elif solver == 'BGD':
            for _ in range(epochs):
                Y_est = self.predict(X)
                # @ = broadcasting
                self.w += (self.eta/p) * ((Y - Y_est) @ X.T).ravel()
                self.b += (self.eta/p) * np.sum(Y - Y_est)
                error_history.append(self.MSE(X, Y))

        # Mini Batch Gradient Descent
        elif solver == 'mBGD':
            for _ in range(epochs):
                mini_batch = self.batcher(X, Y, batch_size)
                for mX, mY in mini_batch:
                    p = mX.shape[1]
                    Y_est = self.predict(mX)
                    # @ = broadcasting
                    self.w += (self.eta/p) * ((mY - Y_est) @ mX.T).ravel()
                    self.b += (self.eta/p) * np.sum(mY - Y_est)

                error_history.append(self.MSE(X, Y))

        # Pseudo-inverse (Direct Method)
        elif solver == "PINV":
            X_hat = np.concatenate((np.ones((1, p)), X), axis=0)
            w_hat = np.dot(Y, np.linalg.pinv(X_hat))
            self.w = w_hat[0, 1:]
            self.b = w_hat[0, 0]

        return error_history


if __name__=="__main__":
    p = 300
    x = -1 + 2 * np.random.rand(p).reshape(1, -1)
    y = ( -x + 19 - 12 ) + np.random.randn(1, p)

    solver = 'PINV'
    neuron = LinearNeuron(1, 0.005)
    print( neuron.w )
    error = neuron.fit(x, y, solver=solver)
    print( neuron.w )

    plt.figure(figsize=(10,6))
    plt.title(solver)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.plot(x, y, '.b')
    xn = np.array([[-1, 1]])
    plt.plot(xn.ravel(), neuron.predict(xn), '--r')
    
    ## MSE
    plt.figure(figsize=(10,6))
    plt.title("Error")
    plt.ylabel("MSE")
    plt.xlabel("Iterations")
    plt.grid(True)
    plt.plot(error)
    plt.show()
