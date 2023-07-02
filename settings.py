import os
from typing import Any Optional

"""
File used to read sensitive credentials from environment variables

The first parameter of os.getenv represents the actual environment variable from our computer

Q: How do I set an environment variable in my terminal?

A: Run the following command to set lets say `POSTGRES_SERVER_HOST`

```commandline
export POSTGRES_SERVER_HOST="localhost"

Q: How do we check if the environment variable is set?

A: Run 

```commandline
printenv POSTGRES_SERVER_HOST
```

```

As a rule of thumb, we set sensitive credentials such as username, password, api keys as environment variables
so they are not exposed in code

The second parameter represents the default, if the environment variable is not found.
"""

OPENAI_KEY: str = os.getenv("OPENAI_KEY", "")
POSTGRES_SERVER_HOST: str = os.getenv("POSTGRES_SERVER_HOST", "localhost")
POSTGRES_SERVER_PORT: int = int(os.getenv("POSTGRES_SERVER_PORT", "5432"))

"""
TODO: Use a postgres database user which only has READ permission
We don't want the openai model to give DELETE / UPDATE commands, and we accidentally execute it
"""
POSTGRES_SERVER_USERNAME: str = os.getenv("POSTGRES_SERVER_USERNAME", "autopostgres")
POSTGRES_SERVER_PASSWORD: str = os.getenv("POSTGRES_SERVER_PASSWORD", "password")
POSTGRES_SERVER_DATABASE: str = os.getenv("POSTGRES_SERVER_DATABASE", "customer_usage_data")