import NextAuth, { NextAuthOptions } from "next-auth";
import { PrismaAdapter } from "@next-auth/prisma-adapter";
import prisma from "@/lib/prisma";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: "678890271244-kc4v08rvfve0075dd8tpdprkkp0kflco.apps.googleusercontent.com",
      clientSecret: "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",
    }),
  ],
  callbacks: {
  },
  debug: true
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
