# Stage 1: Build the app
FROM node:20-alpine as build

WORKDIR /reactjs
COPY package.json package-lock.json .
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

COPY --from=build /reactjs/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
