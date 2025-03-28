import numpy as np
import matplotlib.pyplot as plt

from data import get_data, inspect_data, split_data

data = get_data()
#inspect_data(data)

train_data, test_data = split_data(data)

# Simple Linear Regression
# predict MPG (y, dependent variable) using Weight (x, independent variable) using closed-form solution
# y = theta_0 + theta_1 * x - we want to find theta_0 and theta_1 parameters that minimize the prediction error

# We can calculate the error using MSE metric:
# MSE = SUM (from i=1 to n) (actual_output - predicted_output) ** 2

# get the columns
y_train = train_data['MPG'].to_numpy()
x_train = train_data['Weight'].to_numpy()

y_test = test_data['MPG'].to_numpy()
x_test = test_data['Weight'].to_numpy()

# TODO: calculate closed-form solution
ones_column = np.ones((len(train_data), 1))
matrix_obserwacji = np.concatenate((ones_column, x_train.reshape(-1, 1)), axis=1) #x_train jako kolumna jednowymiarowa, tworzymy macierz m x n + 1 czyli m x 2 z jedynkami po lewej stronie
optimal_parameter_theta = np.linalg.inv(matrix_obserwacji.T @ matrix_obserwacji) @ matrix_obserwacji.T @ y_train #używam wzoru z 1.13 używając macierzy obserwacji, jej transpozycji, odwrotności i treningowego y

theta_best = [0, 0]

print("Closed-form solution theta: " , optimal_parameter_theta)

# TODO: calculate error
ones_column_test = np.ones((len(test_data), 1))
matrix_obserwacji_test = np.concatenate((ones_column_test, x_test.reshape(-1, 1)), axis=1) #x_test jako kolumna jednowymiarowa, tworzę macierz obserwacji, ale tym razem dla danych testowych, by obliczyć błąd

#funkcja kosztu, błąd średnio-kwadratowy
MSE = np.mean((np.square((matrix_obserwacji_test @ optimal_parameter_theta) - y_test))) #np.mean oblicza średnią arytmetyczną

print("Closed-form solution error: " , MSE)

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(optimal_parameter_theta[0]) + float(optimal_parameter_theta[1]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()

# TODO: standardization
#standaryzacja na podstawie podanego wzoru 1.15, sprawiamy, że wartość średnia z populacjid anej zmiennej wynosi 0, a odchylenie standardowe 1
#ustandaryzowane wartości pomogą nam dokonać obliczeń, których nie dałoby się wykonać ze względu na różnice skali zmiennych
x_train_standarized = (x_train - np.mean(x_train))/np.std(x_train)
x_test_standarized = (x_test - np.mean(x_train))/np.std(x_train)
y_train_standarized = (y_train - np.mean(y_train))/np.std(y_train)
y_test_standarized = (y_test - np.mean(y_train))/np.std(y_train)

#macierz obserwacji z ustandaryzowanymi danymi treningowymi x
ones_column2 = np.ones((len(train_data), 1))
matrix_x_train_s = np.concatenate((ones_column2, x_train_standarized.reshape(-1, 1)), axis=1)

# print(x_train_standarized, x_test_standarized, y_train_standarized)


# TODO: calculate theta using Batch Gradient Descent
# gradient - wektor pochodnych cząstkowych funkcji po wszystkich jej argumentach
gradient_theta = np.zeros(2)
gradient_theta[0] = np.random.rand() #początkowo losujemy wartości pomiędzy 0 a 1
gradient_theta[1] = np.random.rand()
learning_rate = 0.001 #wyznaczony optymalny learning rate metodą prób i błędów
length = len(matrix_x_train_s)

#gradient_mse mówi nam, jak powinniśmy zmienić gradient_theta, by dla danego zbioru błąd pomiędzy wartościami rzeczywistymi a predykcją modelu zmniejszył się
#czym bliżej do poprawnej wartości, tym mniejszy jest gradient_mse, co za tym idzie kroki które podejmuje algorytm są również mniejsze, by wyznaczyć jak najbardziej zbliżoną wartość thety
for i in range(16000): #w pętli przybliżamy się do ustandaryzowanej wartości gradient theta
    error = matrix_x_train_s @ gradient_theta - y_train_standarized
    gradient_mse = (2 / length) * (matrix_x_train_s.T @ error)
    gradient_theta = gradient_theta - learning_rate * gradient_mse

#matrix_obserwacji_test = np.ones((x_test_standarized.shape[0],2))
#matrix_obserwacji_test[:,1] = x_test_standarized

#macierz obserwacji dla ustandaryzowanych danych testowych x
ones_column3 = np.ones((len(x_test_standarized), 1))
matrix_obserwacji_test = np.concatenate((ones_column3, x_test_standarized.reshape(-1, 1)), axis=1)

#scaled_theta = gradient_theta.copy()
#scaled_theta[1] = scaled_theta[1] * np.std(y_train) / np.std(x_train)
#scaled_theta[0] = np.mean(y_train) - scaled_theta[1] * np.mean(x_train)
#scaled_theta = scaled_theta.reshape(-1)

print("Gradient Descent theta, standarized: " , gradient_theta)

# TODO: calculate error
y_pred = (matrix_obserwacji_test @ gradient_theta) #obliczamy ustandaryzowaną jeszcze wartość predykcji naszego modelu dla i-tego wektora cech

y_pred_destandarised = y_pred * np.std(y_train) + np.mean(y_train) #odwracamy wzór by zdestandaryzować naszą obliczoną wartość y_pred

#funkcja kosztu, błąd średnio-kwadratowy
MSE2 = np.mean((np.square(y_pred_destandarised - y_test))) #obliczamy rzeczywisty błąd na podstawie zdestandaryzowanych już danych

print("Calculated Gradient Descent error: " , MSE2) #zauważamy, że błąd wychodzi ten sam co w przypadku metody closed-form solution

# plot the regression line
x = np.linspace(min(x_test_standarized), max(x_test_standarized), 100)
y = float(gradient_theta[0]) + float(gradient_theta[1]) * x
plt.plot(x, y)
plt.scatter(x_test_standarized, y_test_standarized)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()