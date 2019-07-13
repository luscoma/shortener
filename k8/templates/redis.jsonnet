local kube = import '../lib/kube.libsonnet';

{
  deployment: kube.Deployment('redis') {
    spec+: {
      replicas: 1,
      template+: {
        spec+: {
          containers_+: {
            web: kube.Container('redis') {
              image: 'redis',
              ports_+: { http: { containerPort: 6379 } },
            },
          },
        },
      },
    },
  },

  service: kube.Service('redis') {
    target_pod: $.deployment.spec.template,
  },
}
