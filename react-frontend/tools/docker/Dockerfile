# ==============================================================================
# Stage 1
# ==============================================================================
FROM node:22-slim AS nodebuild

# copy the react-frontend folder into the container
COPY ./react-frontend /run/react-frontend

# set the working directory to the react-frontend folder
WORKDIR /run/react-frontend

# install the dependencies
RUN yarn install

# build the react app - this will create a build folder (in this case, the folder is named 'dist' since we use vite)
RUN yarn build

# optionally run using the serve package
# # expose the port that serve will listen on
# EXPOSE 8080
# # install the serve package
# RUN yarn global add serve
# # run the serve package with the build folder
# CMD ["serve", "-s", "dist", "-l", "8080"]

# ==============================================================================
# Stage 2
# ==============================================================================
# 2nd stage build that will copy the outputs of the build from the first stage

FROM nginx:alpine

# move the build folder to the default location nginx expects it to be
COPY --from=nodebuild /run/react-frontend/dist /usr/share/nginx/html

# copy the nginx config file to the container
COPY ./react-frontend/tools/docker/nginx.conf /etc/nginx/nginx.conf

# expose the port that nginx will listen on
EXPOSE 8080

# nginx typically runs as daemon - detached from the terminal as a background process
# docker needs some commands to run in the foreground to keep them active
CMD ["nginx", "-g", "daemon off;"]