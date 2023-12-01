import Link from "next/link";
import { ReactNode } from "react";
import ReactMarkdown from "react-markdown";

export default function RepoEntry({
  title,
  description,
  large,
}: {
  title: string;
  description: string;
  demo: ReactNode;
  large?: boolean;
}) {
  return (
    <div
      className={`relative col-span-1 overflow-hidden rounded-xl border border-gray-200 bg-white shadow-md ${
        large ? "md:col-span-2" : ""
      }`}
    >
      {/* <div className="flex h-60 items-center justify-center">{demo}</div> */}
      <div className="">
        <div className="grid grid-cols-3 gap-4">
          <p>{title}</p>

          <p>{description}</p>
        </div>
        {/* <div className="prose-sm mt-3 leading-normal text-gray-500 [text-wrap:balance] md:prose">
          <ReactMarkdown
            components={{
              a: ({ node, ...props }) => (
                <a
                  target="_blank"
                  rel="noopener noreferrer"
                  {...props}
                  className="font-medium text-gray-800 underline transition-colors"
                />
              ),
              code: ({ node, ...props }) => (
                <code
                  {...props}
                  // @ts-ignore (to fix "Received `true` for a non-boolean attribute `inline`." warning)
                  inline="true"
                  className="rounded-sm bg-gray-100 px-1 py-0.5 font-mono font-medium text-gray-800"
                />
              ),
            }}
          >
            {description}
          </ReactMarkdown>
        </div> */}
      </div>
    </div>
  );
}
