import RepoEntry from "@/components/home/repo-entry";
import { DEPLOY_URL } from "@/lib/constants";
import { Github, Twitter } from "@/components/shared/icons";
import WebVitals from "@/components/home/web-vitals";
import ComponentGrid from "@/components/home/component-grid";
import Image from "next/image";
import { nFormatter } from "@/lib/utils";
import { ReactNode, useState } from "react";

export default async function UserHome({ searchParams }:
  { searchParams: { url: string, title: string, description: string } }) {
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
  const base_url = "http://localhost:8000"
  const response = await fetch(base_url+`/user/getRepoInfo?repo_url=${searchParams.url}`).then((res)=>res.json()).catch((e)=>console.log(e))
  const parseDate= (dateStr:string) => {
    const inputDate = new Date(dateStr);

    // Create an array of month names
    const monthNames = [
      "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];

    // Get the month, day, and year components from the Date object
    const month = monthNames[inputDate.getMonth()];
    const day = inputDate.getDate();
    const year = inputDate.getFullYear();

    // Format the date as "month day, year"
    const formattedDate = `${month} ${day}, ${year}`;
    return formattedDate

  }

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
          {response.pullRequests.map((item: any, index: any) => (
            <div key={index}>
              <h2
                className="text-xl font-bold"
                style={{
                  paddingTop: "1rem",
                }}
              >{parseDate(item.created_at)}</h2>
                <div>
                  <strong>{item.title}</strong>
                  <p>{item.description}</p>
                </div>

            </div>
          ))}
        </div>
      </div>

        
    </>
  );
} 