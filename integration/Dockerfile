FROM node:8

# Create app directory and epgpub directory
RUN mkdir /src
WORKDIR /src

# Install app dependencies
COPY package.json /src/package.json
RUN npm install

#Bundle app source
COPY . /src

CMD ["npm", "start"]
