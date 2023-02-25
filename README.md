 - To test this file run :

    ./fetch.py --metadata https://www.google.com https://www.github.com

 - For docker

    docker build -t fetch .
    
    docker run --rm -v $(pwd):/app fetch --metadata https://www.google.com https://www.github.com


