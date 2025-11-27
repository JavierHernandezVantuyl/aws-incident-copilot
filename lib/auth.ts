import { AuthOptions } from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials"

export const authOptions: AuthOptions = {
  providers: [
    CredentialsProvider({
      name: "AWS Credentials",
      credentials: {
        username: { label: "Username", type: "text", placeholder: "your-username" },
        password: { label: "Password", type: "password" },
        awsAccessKeyId: { label: "AWS Access Key ID", type: "text" },
        awsSecretAccessKey: { label: "AWS Secret Access Key", type: "password" },
        awsRegion: { label: "AWS Region", type: "text", placeholder: "us-east-1" },
      },
      async authorize(credentials) {
        // In a real app, you'd verify username/password against a database
        // For now, we'll accept any username/password and store the AWS credentials
        if (!credentials?.username || !credentials?.password) {
          return null
        }

        // Store AWS credentials in the user object
        return {
          id: credentials.username,
          name: credentials.username,
          awsAccessKeyId: credentials.awsAccessKeyId || "",
          awsSecretAccessKey: credentials.awsSecretAccessKey || "",
          awsRegion: credentials.awsRegion || "us-east-1",
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      // Store AWS credentials in the JWT token
      if (user) {
        token.awsAccessKeyId = (user as any).awsAccessKeyId
        token.awsSecretAccessKey = (user as any).awsSecretAccessKey
        token.awsRegion = (user as any).awsRegion
      }
      return token
    },
    async session({ session, token }) {
      // Make AWS credentials available in the session
      if (session.user) {
        (session.user as any).awsAccessKeyId = token.awsAccessKeyId as string
        (session.user as any).awsSecretAccessKey = token.awsSecretAccessKey as string
        (session.user as any).awsRegion = token.awsRegion as string
      }
      return session
    },
  },
  pages: {
    signIn: "/login",
  },
  session: {
    strategy: "jwt",
    maxAge: 24 * 60 * 60, // 24 hours
  },
  secret: process.env.NEXTAUTH_SECRET,
}
