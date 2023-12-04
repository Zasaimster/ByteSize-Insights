import Card from "@/components/home/card";
import { Github, Twitter } from "@/components/shared/icons";
import WebVitals from "@/components/home/web-vitals";
import ComponentGrid from "@/components/home/component-grid";
import Image from "next/image";
import { nFormatter } from "@/lib/utils";

export default async function UserHome() {
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

  return (
    <>
      <div className="z-10 w-full max-w-xl px-5 xl:px-0">
        <h1
          className="animate-fade-up bg-gradient-to-br from-black to-stone-500 bg-clip-text text-center font-display text-4xl font-bold tracking-[-0.02em] text-transparent opacity-0 drop-shadow-sm [text-wrap:balance] md:text-7xl md:leading-[5rem]"
          style={{ animationDelay: "0.15s", animationFillMode: "forwards" }}
        >
          Respositories
        </h1>
      </div>

      <div className="my-10 grid w-full max-w-screen-xl animate-fade-up grid-cols-1 gap-5 px-5 md:grid-cols-3 xl:px-0">
        {features.map(({ title, large }) => (
          <Card
            key={title}
            title={title}
            demo={null}
            // description={description}
            repoTitle={title}
            large={large}
          />
        ))}
      </div>
    </>
  );
}

const features = [
  {
    title: "Linux",
    large: true,
  },
  {
    title: "Byte-Size Insights",
    large: true,
  },
  {
    title: "LLaMa2",
    large: true,
  }
];