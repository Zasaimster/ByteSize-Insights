import Navbar from "./navbar";
import { getServerSession } from "next-auth/next";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import { useSession } from "next-auth/react";
import { useEffect } from "react";
export default async function Nav() {
  return <Navbar />;
}
