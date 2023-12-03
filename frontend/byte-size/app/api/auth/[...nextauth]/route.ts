import NextAuth, { NextAuthOptions } from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";
import { authOptions } from "./authOptions";
const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
