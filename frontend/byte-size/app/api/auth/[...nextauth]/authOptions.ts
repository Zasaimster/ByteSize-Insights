import GoogleProvider from "next-auth/providers/google";
import axios from 'axios'
const url = "http://127.0.0.1:8000"
export const authOptions = {
    providers: [
      GoogleProvider({
        clientId: "678890271244-kc4v08rvfve0075dd8tpdprkkp0kflco.apps.googleusercontent.com",
        clientSecret: "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",
      }),
    ],
    callbacks: {
        async session({session, token, user}) {
            const user_email = session.user.email
            const nameParts = session.user.name.split(" ")
            const firstName = nameParts[0]
            const lastName = nameParts[1]
            const signUpUrl = url + "/auth/signUp"
            const loginUrl = url + "/auth/login"
            // signup
            try {
                const signUpResponse = await axios({
                    method:"post",
                    url: signUpUrl,
                    data: {
                        email: user_email,
                        password: "password",
                        firstName: firstName,
                        lastName: lastName
                    },
                    headers: {
                        "Content-Type": "application/json" // Set the content type to JSON
                    }
                })
            } catch(error) {
                console.log(error)
            }
            try {
                const loginResponse = await axios({
                    method:"post",
                    url: loginUrl,
                    data:{
                        username: user_email,
                        password: "password"
                    },
                    headers:{
                        "Content-Type":"application/x-www-form-urlencoded"
                    }
                })
                session.token = loginResponse.data.access_token
                return session
            } catch(error) {
                console.log(error)
            }
        }
    },
  };