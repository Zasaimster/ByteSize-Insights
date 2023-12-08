<img src="https://therealsujitk-vercel-badge.vercel.app/?app=byte-size-insights" />

# Repository Template

Bytesize Insights is a powerful application that aggregates repository PRs and utilizes ChatGPT to generate concise summaries. The user-friendly front-end interface allows personalized customization of subscribed repositories. Stay informed with weekly email digests detailing the latest happenings in your chosen repositories. Experience streamlined PR management with Bytesize Insights.

## Usage

Visit our [Wiki](https://github.com/Zasaimster/ByteSize-Insights/wiki) for more information regarding application usage.

## Local Development

To work on this locally, first pull the repository. Since this is a monolithic application, we include both the backend and frontend within this repository.

### Frontend

Follow these instructions before writing any code:

- Install Node version 21.x
- Install npm version 10.x
- Navigate to `/frontend/byte-size/` in order to work on the frontend.
- Run `npm install` to install our dependencies
- Run `npm run dev` to load the development server located at `http://localhost:3000`

You will need to be running the backend simultaneously if you would like to walk through user workflows. Check the [Backend](https://github.com/Zasaimster/ByteSize-Insights?tab=readme-ov-file#backend) section to run the server.

### Backend

Follow these instructions before updating the code:

- Install Python 3.12.x
- Install Pip 23.x.
- Run `pip install -r requirements.txt`
- Create a `.env` file with the following fields:

```
MONGO_URI=...
GITHUB_TOKEN=...
OPENAI_TOKEN=...
```

### Lambda Function

Our AWS Lambda function is stored in `/bytesize-insights_cron/lambda_function.py`. Navigate there to update the function. `BACKEND_URL` is stored in the AWS environment field, but it points to where the backend runs. If you would like to test the code, set `BACKEND_URL=http://localhost:8000/` and run the function through the command line.

## Deployment

We use Vercel to handle the deployment process for us. Since this was initially a school project, we were looking for a tool that required the least amount of configuration that could get the application deployed the quickest. Vercel met our requirements because we provide Vercel permissions to access our GitHub repository, removing the need for a continuous deployment script. Instead, our continuous deployment is fully configured through the Vercel dashboard user interface to update whenever code is pushed onto the *main* branch. Additionally, Vercel enables us to run the tests prior to each deployment.

Here are the steps required to set up the Vercel deployment. Once these are completed, continuous deployment is integrated onto the *main* branch.

 1. Navigate to you Vercel account and create a new project. Give it a relevant title like "bytesize-insights-backend"
 2. Link your GitHub account to Vercel and grant it permissions to access your repositories. Select this repository from the list of repositories.
 3. Under "Framework Preset" select "Other" if you are deploying the FastAPI backend, and "Next.js" if you are deploying the frontend. Set the root directory to the corresponding folder (*/backend* or */frontend/byte-size*)
 4. Configure the build settings to run the application. Click deploy and try out your hosted application!

### CI/CD

To deploy this application, simply make changes to the main branch via a pull request. The badge at the beginning of this README indicates the status of the deployment: if the application has been deployed successfully, the badge will be green. This application utilizes Vercel to conduct continuous deployment of the frontend and backend. Similarly, the cron job used to send emails and scrape the GitHub API for pull requests has implicit continuous deployment via changes to the backend API. Whenever changes to the main branch of the repository, Vercel will trigger a new deployment of the frontend, backend, and cron job.

### Lambda Function

The AWS Lambda function is deployed on one of our AWS accounts. The logic is simple and shouldn't be changed, so there should not be a need to adjust this, but contact @Zasaimster (saimm.ahmadd@gmail.com) for more information.
