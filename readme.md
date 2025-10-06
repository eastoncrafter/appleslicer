# AppleSlicer
## A text-based web slicer based off Prusa Slicer CLI


Built using flask, html, python logic, and hopes+dreams

### Main Interface:
![Main Interface screenshot](images/maininterfacev1.png "main interface")

To use:
git clone https://github.com/eastoncrafter/appleslicer  
edit docker compose with continuous print settings, and octoprint api key and all that jazz (api key may not work everywhere yet check into that future me)  
docker compose up -d

Current Issues:
Hardcoded values everywhere
No progress bar, and since it's not streaming progress, and relying on a post request, it's most likely going to timeout if given a long job, especially if ran through a reverse proxy
