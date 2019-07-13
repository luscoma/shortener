local redis = import "./templates/redis.jsonnet";
local shortner = import "./templates/shortner.jsonnet";

{
  redis_deployment: redis.deployment,
  redis_service: redis.service,

  shortner_deployment: shortner.deployment,
  shortner_service: shortner.service+ {
    spec+: {
      type: 'LoadBalancer',
      loadBalancerIP: 'localhost'
    }
  }
}

