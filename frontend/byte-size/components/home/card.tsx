import Link from "next/link";
import { ReactNode } from "react";
import ReactMarkdown from "react-markdown";

export default function Card({
  title,
  demo,
  repoTitle,
  large,
}: {
  title: string;
  demo: ReactNode;
  repoTitle: string;
  large?: boolean;
}) {
  return (
    <div
      className={`relative col-span-1 overflow-hidden rounded-xl border border-gray-200 bg-white shadow-md ${large ? "md:col-span-2" : ""
        }`}
    >
      <div className="">
        <div className="grid grid-cols-3 gap-4">
          <h2 className="col-span-1 bg-gradient-to-br from-black to-stone-500 bg-clip-text font-display text-xl font-bold text-transparent [text-wrap:balance] md:text-3xl md:font-normal">
            {title}
          </h2>
          <button className="col-span-1">Subscribe</button>
          <Link
            href={{
              pathname: '/repos',
              query: { title: title, description: "byte" }
            }}
            className="col-span-1">View</Link>
        </div>
      </div>
    </div>
  );
}
