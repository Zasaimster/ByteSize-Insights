'use client'
import Card from "@/components/home/card";
import { Github, Twitter } from "@/components/shared/icons";
import WebVitals from "@/components/home/web-vitals";
import ComponentGrid from "@/components/home/component-grid";
import Image from "next/image";
import { nFormatter } from "@/lib/utils";
import { useSession } from "next-auth/react";
import { useEffect, useState } from "react";
export default function UserHome() {
  const { data: session } = useSession()
  const [subscribed, setSubscribed] = useState([
    {
      title: "Linux",
      large: true,
    },
    {
      title: "React",
      large: true,
    }
  ]);

  const [repos, setRepos] = useState([
    { title: "MongoDB", large: true },
    { title: "TensorFlow", large: true },
    { title: "VSCode", large: true }
  ]);

  const subscribe = (repo : any) => {
    setSubscribed([...subscribed, repo]);
    setRepos(repos.filter(r => r.title !== repo.title));
  };

  const unsubscribe = (sub: any) => {
    setRepos([...repos, sub]);
    setSubscribed(subscribed.filter(s => s.title !== sub.title));
  };

  // const subscribed = [
  //   {
  //     title: "Linux",
  //     large: true,
  //   },
  //   {
  //     title: "React",
  //     large: true,
  //   }
  // ];


  return (
    <>
      <div className="z-10 w-full max-w-xl px-5 xl:px-0">
        <h1
          className="animate-fade-up bg-gradient-to-br from-black to-stone-500 bg-clip-text text-center font-display text-4xl font-bold tracking-[-0.02em] text-transparent opacity-0 drop-shadow-sm [text-wrap:balance] md:text-7xl md:leading-[5rem]"
          style={{ animationDelay: "0.15s", animationFillMode: "forwards" }}
        >
          Subscribed
        </h1>
      </div>

      <div className="my-10 grid w-full max-w-screen-xl animate-fade-up grid-cols-1 gap-5 px-5 md:grid-cols-3 xl:px-0">
        {subscribed.map(({ title, large }) => (
          <Card
            key={title}
            title={title}
            action="Unsubscribe"
            // description={description}
            onClick={() => unsubscribe({ title, large })}
            repoTitle={title}
            large={large}
          />
        ))}
      </div>

      <div className="z-10 w-full max-w-xl px-5 xl:px-0">
        <h1
          className="animate-fade-up bg-gradient-to-br from-black to-stone-500 bg-clip-text text-center font-display text-4xl font-bold tracking-[-0.02em] text-transparent opacity-0 drop-shadow-sm [text-wrap:balance] md:text-7xl md:leading-[5rem]"
          style={{ animationDelay: "0.15s", animationFillMode: "forwards" }}
        >
          All Repos
        </h1>
      </div>

      <div className="my-10 grid w-full max-w-screen-xl animate-fade-up grid-cols-1 gap-5 px-5 md:grid-cols-3 xl:px-0">
        {repos.map(({ title, large }) => (
          <Card
            key={title}
            title={title}
            action="Subscribe"
            onClick={() => subscribe({ title, large })}
            // description={description}
            repoTitle={title}
            large={large}
          />
        ))}
      </div>
    </>
  );
}