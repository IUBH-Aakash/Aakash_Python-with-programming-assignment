from sqlalchemy import create_engine, Table, Column, String, Float, MetaData

def write_deviation_results_to_sqlite(result):
    """
    It will write results in sqllite db of classification computation
    :parameter result: Result of a classification test
    """
    # We will use SQLAlchemy. In this Metadata is used to describe the tables and columns
    engine = create_engine('sqlite:///{}.db'.format("mapping"), echo=False)
    metadata = MetaData(engine)

    mapping = Table('mapping', metadata,
                    Column('X (test func)', Float, primary_key=False),
                    Column('Y (test func)', Float),
                    Column('Delta Y (test func)', Float),
                    Column('No. of ideal func', String(50))
                    )

    metadata.create_all()

    # Using SQLAlchemy's .execute dictionary to contain all the values. Because injecting the values line by line takes lot of time. And time is precious so it should be saved to invest later.
    execute_map = []
    for item in result:
        point = item["point"]
        classification = item["classification"]
        delta_y = item["delta_y"]

        # To be compliant we will now test if there is a classification for a point. If its there then we will rename the function name.
        classification_name = None
        if classification is not None:
            classification_name = classification.name.replace("y", "N")
        else:
            # I write dash in the case where there is no classification so there is no distance.
            classification_name = "-"
            delta_y = -1

        execute_map.append(
            {"X (test func)": point["x"], "Y (test func)": point["y"], "Delta Y (test func)": delta_y,
             "No. of ideal func": classification_name})

    # We will use the dictionary to insert the data by using the Table object.
    i = mapping.insert()
    i.execute(execute_map)