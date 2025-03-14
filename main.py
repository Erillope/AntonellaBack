try:
    with open(r"C:\Users\USER\Documents\VsCode\antonella_definitivo\AntonellaBack\resources\media\a.png", "rb") as f:
        print("¡El archivo se pudo abrir!")
except Exception as e:
    print(f"Error: {e}")