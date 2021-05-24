# Use the Nginx image
FROM nginx

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Replace with our own nginx.conf
COPY nginx.conf /etc/nginx/conf.d/

# copy run.sh
COPY ./run.sh .

# run entrypoint.sh
ENTRYPOINT ["run.sh"]