from dataclasses import fields, is_dataclass
from typing import Any, Dict, Type, get_type_hints


class ValidationError(Exception):
    """Custom validation error"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(message)

def validate_dataclass_data(dataclass_type: Type, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate data against a dataclass schema
    Returns validated data or raises ValidationError
    """
    if not is_dataclass(dataclass_type):
        raise ValueError("dataclass_type must be a dataclass")
    
    # Get all required fields from dataclass
    dataclass_fields = {f.name: f for f in fields(dataclass_type)}
    type_hints = get_type_hints(dataclass_type)
    
    validated_data = {}
    errors = []
    
    # Check required fields
    for field_name, field_obj in dataclass_fields.items():
        if field_name not in data:
            # Check if field has default value
            if field_obj.default is not field_obj.default_factory:
                validated_data[field_name] = field_obj.default
            elif field_obj.default_factory is not field_obj.default_factory:
                validated_data[field_name] = field_obj.default_factory()
            else:
                errors.append(f"Field '{field_name}' is required")
                continue
        else:
            # Validate field type
            expected_type = type_hints.get(field_name)
            value = data[field_name]
            
            try:
                validated_value = validate_field_type(value, expected_type, field_name)
                validated_data[field_name] = validated_value
            except ValidationError as e:
                errors.append(e.message)
    
    if errors:
        raise ValidationError(f"Validation errors: {'; '.join(errors)}")
    
    return validated_data

def validate_field_type(value: Any, expected_type: Type, field_name: str) -> Any:
    """Validate individual field type"""
    if expected_type is None:
        return value
    
    # Handle Optional types (Union[T, None])
    if hasattr(expected_type, '__origin__') and expected_type.__origin__ is type(None):
        if value is None:
            return None
        # Get the non-None type
        args = expected_type.__args__
        non_none_types = [arg for arg in args if arg is not type(None)]
        if non_none_types:
            expected_type = non_none_types[0]
    
    # Basic type validation
    if expected_type in (int, float, str, bool):
        if not isinstance(value, expected_type):
            try:
                # Try to convert
                if expected_type == int:
                    return int(value)
                elif expected_type == float:
                    return float(value)
                elif expected_type == str:
                    return str(value)
                elif expected_type == bool:
                    if isinstance(value, str):
                        return value.lower() in ('true', '1', 'yes', 'on')
                    return bool(value)
            except (ValueError, TypeError):
                raise ValidationError(
                    f"Field '{field_name}' must be of type {expected_type.__name__}, got {type(value).__name__}",
                    field_name
                )
    
    return value

def create_error_response(error: ValidationError) -> Dict[str, Any]:
    """Create standardized error response"""
    return {
        "error": "Validation Error",
        "message": error.message,
        "field": error.field if hasattr(error, 'field') else None
    } 