import RepoEntry from "@/components/home/repo-entry";
import { DEPLOY_URL } from "@/lib/constants";
import { Github, Twitter } from "@/components/shared/icons";
import WebVitals from "@/components/home/web-vitals";
import ComponentGrid from "@/components/home/component-grid";
import Image from "next/image";
import { nFormatter } from "@/lib/utils";
import { ReactNode, useState } from "react";

export default async function UserHome({ searchParams }:
  { searchParams: { title: string, description: string } }) {
  const { stargazers_count: stars } = await fetch(
    "https://api.github.com/repos/Zasaimster/ByteSize-Insights",
    {
      ...(process.env.GITHUB_OAUTH_TOKEN && {
        headers: {
          Authorization: `Bearer ${process.env.GITHUB_OAUTH_TOKEN}`,
          "Content-Type": "application/json",
        },
      }),
      // data will revalidate every 24 hours
      next: { revalidate: 86400 },
    },
  )
    .then((res) => res.json())
    .catch((e) => console.log(e));

  const repo = [
    {
      url: "https://api.github.com/repos/facebook/react/pulls/27776",
      title: "Fix useSyncExternalStoreWithSelector to not call selectors when snapshot hasn't changed",
      updated_at: "2023-12-03T13:40:35Z",
      description: "This pull request addresses a bug in the current implementation of the `useSyncExternalStoreWithSelector` function in React that causes unnecessary re-evaluation of selectors even when the snapshot hasn't changed. This can lead to increased CPU usage, especially in large apps with many selectors and frequent actions. The pull request includes a test that fails in the current version but passes with the fix. It also includes a code diff that shows the changes made to the function. The pull request is currently open and was created on December 2, 2023, and last updated on December 3, 2023.",
    },
    {
      title: "Refactor deployment script for enhanced readability and robustness",
      updated_at: "2023-12-01T22:16:56Z",
      description: "This pull request aims to refactor the deployment script for improved readability and robustness. The main function has been modularized into smaller, focused functions, making the code easier to understand and maintain. Error handling has been implemented to catch and report any unhandled exceptions, enhancing the script's robustness. User interaction has been improved with clearer instructions and outputs, making the script more user-friendly. Comprehensive comments have been added to provide context and understanding of the code logic. Sensitive data and tokens are now handled securely to prevent potential security risks. These changes were tested in various scenarios, including valid and invalid inputs, error simulations, and successful execution verification. A peer review was conducted for further validation. This PR is currently open and was created on 2023-12-01 at 21:34:06 UTC. The last update was made on 2023-12-01 at 22:16:56 UTC."
    },
    {
      title: "Move client only exports to `react-dom/client`",
      updated_at: "2023-12-01T22:16:16Z",
      description: "This pull request moves the client only exports to `react-dom/client` to avoid conflicts with the new `react-dom/server` module. The pull request also updates the documentation to reflect the new location of these exports. This pull request is currently open and was created on 2023-12-01 at 21:34:06 UTC. The last update was made on 2023-12-01 at 22:16:16 UTC."
    },
    {
      title: "[Fizz] Add Component Stacks to `onError` and `onPostpone` when in dev mode or during prerenders in prod mode",
      updated_at: "2023-12-01T22:16:16Z",
      description: "This pull request adds component stacks to `onError` and `onPostpone` when in dev mode or during prerenders in prod mode. This is useful for debugging purposes as it allows developers to see which component caused an error or was postponed. The pull request also includes a test that verifies the changes. This pull request is currently open and was created on 2023-12-01 at 21:34:06 UTC. The last update was made on 2023-12-01 at 22:16:16 UTC."
    },
    {
      title: "GitHub actions and workflows",
      updated_at: "2023-12-01T22:16:16Z",
      description: "This pull request adds GitHub actions and workflows to the project. This allows for automated testing and deployment of the project. The pull request also includes a test that verifies the changes. This pull request is currently open and was created on 2023-12-01 at 21:34:06 UTC. The last update was made on 2023-12-01 at 22:16:16 UTC."
    },
    {
      url: "https://api.github.com/repos/facebook/react/pulls/27750",
      title: "Update attribute-behavior fixture app to latest React + React Scripts",
      description: "This pull request is titled 'Update attribute-behavior fixture app to latest React + React Scripts' and it aims to update the attribute-behavior fixture app to the latest versions of React and react-scripts. This update was necessary as the old versions were causing difficulties in running the app locally. The dependencies have been upgraded and the markdown fixture generation has been re-run. The changes made have also resolved some issues related to form attributes. The change was tested by running `yarn dev` and ensuring that the app launches and renders properly. The ability to save markdown fixtures was also tested, with a diff provided in the pull request. The pull request is currently open and was created on 2023-11-27 at 19:27:25Z. It was last updated on 2023-11-27 at 21:51:26Z.",
      updated_at: "2023-12-03T13:40:35Z"
    }
  ]


  const data: { date: string, pullRequests: { pullRequest: string, description: string }[] }[] = [
    {
      date: "01/08/2023",
      pullRequests: [
        {
          pullRequest: "Feature Enhancement",
          description: "This Pull Request introduces a new feature that enhances the user experience of our app. It includes improved navigation, a sleeker user interface, and faster performance. This feature will make it easier for users to explore and interact with our platform."
        },
        {
          pullRequest: "Bug Fix",
          description: "This Pull Request addresses a critical bug that was causing unexpected crashes in our application. It includes a comprehensive fix for the issue, along with thorough testing to ensure the problem is resolved. Users will now experience a more stable and reliable app."
        },
        {
          pullRequest: "Documentation Update",
          description: "This Pull Request updates our documentation to reflect the latest changes and features in our app. It includes revised user guides, API documentation, and code comments. Keeping our documentation up to date is essential for helping developers and users understand our software."
        },
        {
          pullRequest: "Performance Optimization",
          description: "This Pull Request focuses on optimizing the performance of our app. It includes code refactoring, caching improvements, and database query optimizations. As a result, our app will load faster and respond more efficiently to user actions."
        },
        {
          pullRequest: "New Feature - Social Sharing",
          description: "This Pull Request introduces a brand new feature that allows users to easily share their achievements and activities on social media platforms."
        }
      ]
    },
    {
      date: "01/07/2023",
      pullRequests: [
        {
          pullRequest: "Feature Enhancement",
          description: "This Pull Request introduces a new feature that enhances the user experience of our app. It includes improved navigation, a sleeker user interface, and faster performance. This feature will make it easier for users to explore and interact with our platform."
        }
      ]
    }
  ];

  return (
    <>
      <div className="z-10 w-full max-w-screen-xl px-5 xl:px-0">
        <h1
          className="animate-fade-up bg-gradient-to-br from-black to-stone-500 bg-clip-text text-center font-display text-4xl font-bold tracking-[-0.02em] text-transparent opacity-0 drop-shadow-sm [text-wrap:balance] md:text-7xl md:leading-[5rem]"
          style={{ animationDelay: "0.15s", animationFillMode: "forwards" }}
        >
          {searchParams.title}
        </h1>

        {/* A filter to show items from the repo array, ordered by date in descending or ascending order, with a dropdown */}


        <div>
          {repo.map((item, index) => (
            <div key={index}>
              <h2
                className="text-xl font-bold"
                style={{
                  paddingTop: "1rem",
                }}
              >{item.updated_at}</h2>
              <p
                className="font-bold"
                style={{
                  paddingTop: "1rem",
                }}>
                {item.title}
              </p>

              <p>
                {item.description}
              </p>
            </div>
          ))}
        </div>
      </div>

        
    </>
  );
} 