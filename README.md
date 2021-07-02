
# Fetch Rewards Coding Assessment - DevOps Engineer

Develop an automation program that takes a YAML configuration file as input and deploys a Linux AWS EC2 instance with two volumes and two users.

---

## Requirements

>To run this pythonic program you will need an AWS user with the proper permissions as well as Python - [download](https://www.python.org/downloads)

Prior to running the python script(s), you will need to first create a `.env` file in the root directory.

:bulb: The following code snippets will assume that you downloaded the repo zip and that you have already unzipped it in your `Downloads` directory. The unzipped repo folder name is `fetchrewards-coding-assessment-main`

After downloading or cloning this repo, open the terminal app of your choice. In the terminal, type the following command to `cd` into the root directory:

```sh
cd ~/Downloads/fetchrewards-coding-assessment-main
```

Inside the root directory, we will now create a `.env` file by copying `.env.example`. Here's the terminal command to do that:

```sh
cp .env.example .env
```

### Environment Variables

With our `.env` file created, we now need to paste in the values for the following environment variables: `AWS_ACCESS_TOKEN_ID`, `AWS_SECRET_ACCESS_TOKEN`, and `AWS_REGION`.

![Environment Var Example](/images/env-example.png)

After pasting your variables in, your `.env` file should similar to this:

![Environment Var Example Comp](images/env-example-comp.png)

## Deployment

With python downloaded, our `.env` created, and our environment variables set, we can finally run the program with the following command:

```shell
  python3.9 cli.py
```
  
## License

[MIT](https://choosealicense.com/licenses/mit/)
