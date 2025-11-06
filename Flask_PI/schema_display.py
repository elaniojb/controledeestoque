from sqlalchemy import create_engine, MetaData
from sqlalchemy_schemadisplay import create_schema_graph

engine = create_engine('sqlite:///instance/database.db')
metadata = MetaData()
metadata.reflect(bind=engine)

graph = create_schema_graph(metadata=metadata, engine=engine)
graph.write_png("schema.png")  # Gera o diagrama ER
