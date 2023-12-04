import Navbar from "./navbar";
import { getServerSession } from "next-auth/next";
import { useSession } from "next-auth/react";
import { useEffect } from "react";
export default async function Nav() {
  return <Navbar />;
}
