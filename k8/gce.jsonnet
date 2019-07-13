local redis = import './templates/redis.jsonnet';
local shortner = import './templates/shortner.jsonnet';

{
  redis_deployment: redis.deployment,
  redis_service: redis.service,

  shortner_deployment: shortner.deployment,
  shortner_service: shortner.service+ {
    spec+: { type: 'NodePort', }
  },

  shortner_ingress: {
    apiVersion: 'extensions/v1beta1',
    kind: 'Ingress',
    metadata: {
      name: 'shortner-ingress',
      annotations: {
        "kubernetes.io/ingress.global-static-ip-name": "shortner-static-ip",
        // Enable ACME for letsencrypt certificate issuance
        "certmanager.k8s.io/cluster-issuer": "letsencrypt-prod",
        "certmanager.k8s.io/acme-http01-edit-in-place": "true"
      }
    },
    spec: {
      tls: [{
        hosts: [ "whut.page" ],
        secretName: "www-whut-page-tls"
      }],
      backend: {
        serviceName: $.shortner_service.metadata.name,
        servicePort: 8080,
      },
    },
  },
}
