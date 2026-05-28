# Dockerfile.C - cả hai: CMD làm default args cho ENTRYPOINT
FROM alpine
ENTRYPOINT ["echo"]
CMD ["default-msg"]
