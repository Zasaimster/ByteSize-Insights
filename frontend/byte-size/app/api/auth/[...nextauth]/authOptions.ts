import GoogleProvider from "next-auth/providers/google";
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