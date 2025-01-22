

def copy_model_attributes(data: dict, model_to):
    """Копирование аттрибутов из словаря в модель"""
    for key, value in data.items():
        if value is not None:
            setattr(model_to, key, value)
