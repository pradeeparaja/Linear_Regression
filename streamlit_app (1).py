


import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score , mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('/content/insurance.csv')

df.shape

"""#Exploratory Data Analysis"""

df.isnull().sum()

df.duplicated().sum()

df.drop_duplicates(inplace=True)

df.describe()

df.dtypes

plt.pie(df['sex'].value_counts(),labels=df['sex'].value_counts().index,autopct='%1.2f%%')

plt.pie(df['smoker'].value_counts(),labels=df['smoker'].value_counts().index,autopct='%1.2f%%')

sns.barplot(x=df['region'].value_counts().index,y=df['region'].value_counts())

sns.barplot(x=df['children'].value_counts().index,y=df['children'].value_counts())

"""# Categorical column encoding

"""

cat_cols = df.select_dtypes(include = 'object').columns

cat_cols

encoder = OneHotEncoder(drop='first', sparse_output=False)

encoded = pd.DataFrame(
    encoder.fit_transform(df[cat_cols]),
    columns=encoder.get_feature_names_out(cat_cols)
)

encoded.index = df.index

df = pd.concat([df.drop(columns=cat_cols), encoded], axis=1)

df.head()

df.isnull().sum()

num_cols = ['age', 'bmi', 'children', 'charges']


scaler = StandardScaler()


df[num_cols] = scaler.fit_transform(df[num_cols])

df.head()

for col in num_cols:
    plt.figure(figsize=(8, 4))
    sns.boxplot(x=df[col])
    plt.title(f"Boxplot of {col}")
    plt.show()

Q1 = df[num_cols].quantile(0.25)
Q3 = df[num_cols].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df[num_cols] = df[num_cols].clip(lower=lower_bound, upper=upper_bound, axis=1)

print("Data shape after capping outliers:", df.shape)

"""#Multicollinearity"""

corr_matrix = df[num_cols].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.show()

from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

X = df[num_cols]
X = add_constant(X)

vif = pd.DataFrame()
vif['Features'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print(vif)

"""#Split Features and Target"""

X = df.drop('charges', axis=1)
y = df['charges']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LinearRegression()
model.fit(X_train_scaled, y_train)

"""#Evaluation Metrics"""

y_pred = model.predict(X_test_scaled)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)

print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')
print(f'Root Mean Squared Error: {rmse}')
print(f'R-squared: {r2}')

"""#Visualize Prediction vs Actuals"""

plt.figure(figsize=(8, 6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r')
plt.title('Actual vs Predicted Charges')
plt.xlabel('Actual Charges')
plt.ylabel('Predicted Charges')
plt.show()

df

model.score(X_test_scaled,y_test)

