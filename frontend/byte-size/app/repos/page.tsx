import RepoEntry from "@/components/home/repo-entry";
import { DEPLOY_URL } from "@/lib/constants";
import { Github, Twitter } from "@/components/shared/icons";
import WebVitals from "@/components/home/web-vitals";
import ComponentGrid from "@/components/home/component-grid";
import Image from "next/image";
import { nFormatter } from "@/lib/utils";
import { ReactNode } from "react";

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
      <div className="z-10 w-full max-w-xl px-5 xl:px-0">
        <h1
          className="animate-fade-up bg-gradient-to-br from-black to-stone-500 bg-clip-text text-center font-display text-4xl font-bold tracking-[-0.02em] text-transparent opacity-0 drop-shadow-sm [text-wrap:balance] md:text-7xl md:leading-[5rem]"
          style={{ animationDelay: "0.15s", animationFillMode: "forwards" }}
        >
          {searchParams.title}
        </h1>

        <div>
          {data.map((item, index) => (
            <div key={index}>
              <h2
                className="text-xl font-bold"
                style={{
                  paddingTop: "1rem",
                }}
              >{item.date}</h2>
              {item.pullRequests.map((pr, prIndex) => (
                <div key={prIndex}>
                  <strong>{pr.pullRequest}</strong>
                  <p>{pr.description}</p>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>

      /*
        This takes all the data in the data array and maps it to a RepoEntry component.
      */

        
    </>
  );
}