FROM node:18-bullseye

COPY ./site/ /app

WORKDIR /app

RUN npm install express pg cors

CMD ["node", "server.js"]