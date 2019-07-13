local kube = import '../lib/kube.libsonnet';

{
  deployment: kube.Deployment('shortner-web') {
    spec+: {
      replicas: 3,
      template+: {
        spec+: {
          containers_+: {
            web: kube.Container('shortner-web') {
              image: 'luscoma/shortner:latest',
              ports_+: { http: { containerPort: 8080 } },
            },
          },
        },
      },
    },
  },

  service: kube.Service('shortner-web') {
    target_pod: $.deployment.spec.template,
  },
}
