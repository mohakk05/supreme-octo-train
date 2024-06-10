if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    import pandas as pd
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error
    import mlflow
    # Specify your transformation logic here
    mlflow.set_tracking_uri("http://mlflow:5000/")
    mlflow.set_experiment("hw3")
    filename='data/yellow_tripdata_2023-03.parquet'
    df=pd.read_parquet(filename)
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)
    target = 'duration'
    y_train = df[target].values
    with mlflow.start_run():
        
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        print(lr.intercept_)
        mlflow.sklearn.save_model(model, "hw3-linear-regression")

        y_pred = lr.predict(X_train)
        return lr


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
