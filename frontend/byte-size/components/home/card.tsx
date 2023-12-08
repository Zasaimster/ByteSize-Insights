import Link from "next/link";
import { ReactNode } from "react";
import ReactMarkdown from "react-markdown";

export default function Card({
  title,
  action,
  onClick,
  repoTitle,
  large,
  url
}: {
  title: string;
  action: string;
  onClick?: (title: any) => void;
  repoTitle: string;
  large?: boolean;
  url: string;
}) {
  return (
    <div
      className={`relative col-span-1 p-3 overflow-hidden rounded-xl border border-gray-200 bg-white shadow-md ${large ? "md:col-span-2" : ""
        }`}
    >
      <div className="">
        <div className="grid grid-cols-3 gap-4">
          <h2 className="col-span-1 bg-gradient-to-br from-black to-stone-500 bg-clip-text font-display text-xl font-bold text-transparent [text-wrap:balance] md:text-3xl md:font-normal">
            {title}
          </h2>
          <button className="col-span-1" onClick={onClick}>{action}</button>
          <Link
            href={{
              pathname: '/repos',
              query: { url, title, repoTitle }
            }}
            className="col-span-1 flex items-center justify-center">View</Link>
        </div>
      </div>
    </div>
  );
}
