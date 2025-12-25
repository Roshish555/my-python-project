# Ontology + Python

Keep these files in the SAME folder:

assignment.py  
Assisgnment.rdf  

The ontology file is loaded automatically using:

```python
self.rdf_path = os.path.join(os.path.dirname(__file__), "Assisgnment.rdf")
