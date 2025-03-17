class AccountError(Exception):
    """Excepción base para errores en la creación de cuentas."""

    pass


class InvalidAccountDataError(AccountError):
    """Error para datos de cuenta inválidos."""

    def __init__(
        self, message="Datos de cuenta inválidos. Verifica los valores proporcionados."
    ):
        super().__init__(message)


class DatabaseConnectionError(AccountError):
    """Error para fallos en la conexión con la base de datos."""

    def __init__(self, message="Error en la conexión con la base de datos."):
        super().__init__(message)


class AccountCreationError(AccountError):
    """Error específico durante la creación de la cuenta."""

    def __init__(self, detail="Error al intentar crear la cuenta."):
        super().__init__(detail)


class DuplicateEmailError(AccountError):
    """Excepción para manejar el caso de correos duplicados."""

    def __init__(
        self, message="El correo electrónico ya está registrado en la base de datos."
    ):
        super().__init__(message)
