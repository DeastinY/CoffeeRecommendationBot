# CoffeeRecommendationBot
Recommends a coffee to Twitterusers in need !  
[![Build Status](https://travis-ci.org/DeastinY/CoffeeRecommendationBot.svg?branch=master)](https://travis-ci.org/DeastinY/CoffeeRecommendationBot)

You can see a version of this bot running [here](https://twitter.com/aacoffeebot). I'm still struggling with the automatic responses, but the daily coffee tweet is working great !

![Screenshot of CoffeeRecommendationBot in action](https://github.com/DeastinY/CoffeeRecommendationBot/blob/master/coffeebot.png?raw=true)

## Features
- Responds to direct mentions
- Likes / Retweets indirect mentions
- Can tweet a "Coffee of the Day" style tweet
- Updates it's beverages from Starbucks (Thanks to [@emorres25](https://github.com/emorres25) !)
- Manages drinks in easy-to-edit JSON format (Thanks to [@tsonnen](https://github.com/tsonnen) !)
- Constant quality checks with Travis-CI (Thanks to [@Twista](https://github.com/Twista) !)
- Well maintained code, written with lot's of love (Thanks to everyone !)

## Setup
Install the requirements with `pip install -r requirements.txt`

Create a `keys.py` file with the required tokens:
  >consumer_key=""  
  consumer_secret=""  
  access_token_key=""  
  access_token_secret=""  


## Testing

### [Travis CI](https://travis-ci.org)

Configuration for Travis CI can be found inside `.travis.yml`. The demo version of this bot runs on `Python 2.7`.

If you want travis to use other Python versions like `3.3` you can simply change the `python:` line inside `.travis.yml`

**`.travis.yml` Python 3.3 Sample** 
```yml
language: python

python:
  - 3.3

install:
  - pip install -r requirements.txt
  - pip install pep8 flake8
  - pip list

script:
  - flake8 .
```

You can even test for multiple Python environments (2.7 & 3.3 in the sample below):smile:

**`.travis.yml` Python 2.7 & 3.3 Sample** 
```yml
language: python

python:
  - 2.7
  - 3.3

install:
  - pip install -r requirements.txt
  - pip install pep8 flake8
  - pip list

script:
  - flake8 .
```

## Contribution Guidelines
Thanks for the interest !
Contributing guidelines are available in '[CONTRIBUTING.md](CONTRIBUTING.md)'

## License
This project is licensed under the terms of the MIT license. The full license text is available in the [LICENSE](LICENSE) file.
