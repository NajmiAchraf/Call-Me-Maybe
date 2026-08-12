from __future__ import annotations

import argparse
import json
import math
import os
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Literal

import numpy as np
from pydantic import BaseModel, Field

from .functions import (
    fn_add_numbers,
    fn_get_square_root,
    fn_greet,
    fn_reverse_string,
    fn_substitute_string_with_regex,
)
from .models import (
    FunctionDefinition,
    FunctionTests,
    ParameterSpec,
    ReturnSpec,
    ToolCall,
)
from .parser import parse_args
from .router import ToolRouter
from .x_json_loader import (
    load_functions_definitions,
    load_prompts,
)

__all__ = [
    "annotations",
    "argparse",
    "Path",
    "Any",
    "Callable",
    "Dict",
    "List",
    "Literal",
    "json",
    "BaseModel",
    "Field",
    "np",
    "os",
    "math",
    "re",
]


__all__ += [
    # classes
    "FunctionDefinition",
    "FunctionTests",
    "ParameterSpec",
    "ReturnSpec",
    "ToolCall",
    "ToolRouter",
    # functions
    "fn_add_numbers",
    "fn_get_square_root",
    "fn_greet",
    "fn_reverse_string",
    "fn_substitute_string_with_regex",
    "parse_args",
    "load_functions_definitions",
    "load_prompts",
]
