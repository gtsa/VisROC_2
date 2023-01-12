 #!/bin/bash

if type pip3
then
    echo "pip3 found"
else
    apt-get install python3-pip
    echo "pip3 installed"
fi

if /usr/bin/python3 -m venv venv
then
    echo "venv created with system's python"
else
    python3 -m venv venv
    echo "venv created"
fi

if source venv/bin/activate
then
    echo "venv activated"
else
    echo "venv NOT activated"
fi

if pip3 install -r requirements.txt
then
    echo "required modules installed"
else
    echo "Unable to install required modules"
fi

