# lambda_jinja_sample
Sample of lambda function with Jinja2

# Setup

## Requirements

 * Install Apex for lambda deployment
   * http://apex.run/

## Setup development

```bash
git clone git@github.com:pistatium/lambda_jinja_sample.git
cd lambda_jinja_sample
pip install -r requirements.txt
```

## Deploy
```
pip install -r requirements.txt -t functions/sample
apex deploy
apex invoke jinja
```
