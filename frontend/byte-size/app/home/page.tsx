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
  const url = "http://localhost:8000"
  const [subscribed, setSubscribed] = useState([]);

  const [repos, setRepos] = useState([]);
  const subscribe = (repo: any) => {
    const apiURL = new URL(url + '/user/subscribeToRepo')
    apiURL.searchParams.append('repo_url', repo.url)
    setSubscribed([...subscribed, repo])
    fetch(apiURL.toString(), {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${session.token}`,
        'Content-Type':'application/json'
      }
    })
  };
  useEffect(()=>{
    getRepos()
    getSubscribedRepos()
  },[session])
  const getRepos = async () => {
    const repoList = await fetch(url + "/user/getAllRepos").then((res)=>res.json()).catch((e)=>console.log(e))
    console.log(repoList)
    setRepos(repoList)
  }
  const getSubscribedRepos = async () => {
    const subscribedList = await fetch(url + "/user/getSubbedRepos",{
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${session?.token ?? "placeholder"}`,
        'Content-Type': 'application/json'
      }
    }).then((res)=>res.json()).catch((e)=>console.log(e))
    if (Array.isArray(subscribedList)) {
      setSubscribed(subscribedList)
    }
    
  }
  return (
    <>
    {session && (
      <div>
      <div className="z-10 w-full max-w-xl px-5 xl:px-0">
        <h1
          className="animate-fade-up bg-gradient-to-br from-black to-stone-500 bg-clip-text text-center font-display text-4xl font-bold tracking-[-0.02em] text-transparent opacity-0 drop-shadow-sm [text-wrap:balance] md:text-7xl md:leading-[5rem]"
          style={{ animationDelay: "0.15s", animationFillMode: "forwards" }}
        >
          Subscribed
        </h1>
      </div>

      <div className="my-10 grid w-full max-w-screen-xl animate-fade-up grid-cols-1 gap-5 px-5 md:grid-cols-3 xl:px-0">
        {subscribed.map((item) => (
            <Card
              key={item.name}
              title={item.name}
              action="Subscribe"
              onClick={() => subscribe(item)}
              // description={description}
              repoTitle={item.name}
              large={true}
              url={item.url}
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
        {repos.map((item) => (
          <Card
            key={item.name}
            title={item.name}
            action="Subscribe"
            onClick={() => subscribe(item)}
            // description={description}
            repoTitle={item.name}
            large={true}
            url={item.url}
          />
        ))}
      </div>
      </div>
      )}
    </>
  );
}

const features = [
  {
    title: "Linux",
    large: true,
  },
  {
    title: "React",
    large: true,
  },
  {
    title: "VSCode",
    large: true,
  }
];
