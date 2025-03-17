from app.core.config import supabase


def test_connection():
    """Prueba la conexión obteniendo datos de la tabla 'users'"""
    try:
        response = supabase.table("users").select("*").limit(1).execute()
        print("Conexión exitosa:", response)
        return {"status": "Conexión exitosa", "data": response.data}
    except Exception as e:
        print("Error detallado en la conexión:", str(e))
        return {"status": "Error en la conexión", "error": str(e)}
