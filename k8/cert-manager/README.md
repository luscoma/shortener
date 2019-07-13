# Installation of cert-manager

Used to manage certs, specifically useful for letsencrypt certs.  Common for use on GCE.

## Installing cert-manager

We install it to a custom namespace just so it's by itself

```
kubectl create namespace cert-manager
kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.8.1/cert-manager.yaml
```

## Using lets-encrypt

The letsencrypt issurer must be installed then add the annotations to your ingress

```
certmanager.k8s.io/cluster-issuer: letsencrypt-prod
certmanager.k8s.io/acme-http01-edit-in-place: "true"
```

Your ingress's secret name will become your cert's secret name.  It really does take like 20m for the cert to show
up.  It takes ~10m for the cert to get issues and another ~5m for the ingress point to pick it up.

A successful request looks something like this:

```
alusco@Holo-PC ~/s/k/cert-manager> kubectl describe certificate www-whut-page-tls
Name:         www-whut-page-tls
Namespace:    default
Labels:       <none>
Annotations:  <none>
API Version:  certmanager.k8s.io/v1alpha1
Kind:         Certificate
Metadata:
  Creation Timestamp:  2019-07-13T21:15:36Z
  Generation:          1
  Owner References:
    API Version:           extensions/v1beta1
    Block Owner Deletion:  true
    Controller:            true
    Kind:                  Ingress
    Name:                  shortner-ingress
    UID:                   a9d23c1d-a5a9-11e9-9cb3-42010a80001c
  Resource Version:        156231
  Self Link:               /apis/certmanager.k8s.io/v1alpha1/namespaces/default/certificates/www-whut-page-tls
  UID:                     5bc45af0-a5b3-11e9-9cb3-42010a80001c
Spec:
  Acme:
    Config:
      Domains:
        whut.page
      http01:
        Ingress:  shortner-ingress
  Dns Names:
    whut.page
  Issuer Ref:
    Kind:       ClusterIssuer
    Name:       letsencrypt-prod
  Secret Name:  www-whut-page-tls
Status:
  Conditions:
    Last Transition Time:  2019-07-13T21:23:19Z
    Message:               Certificate is up to date and has not expired
    Reason:                Ready
    Status:                True
    Type:                  Ready
  Not After:               2019-10-11T20:23:18Z
Events:
  Type    Reason              Age   From          Message
  ----    ------              ----  ----          -------
  Normal  Generated           15m   cert-manager  Generated new private key
  Normal  GenerateSelfSigned  15m   cert-manager  Generated temporary self signed certificate
  Normal  OrderCreated        15m   cert-manager  Created Order resource "www-whut-page-tls-1186729136"
  Normal  OrderComplete       8m    cert-manager  Order "www-whut-page-tls-1186729136" completed successfully
  Normal  CertIssued          8m    cert-manager  Certificate issued successfully
```

## References

* https://docs.cert-manager.io/en/latest/getting-started/install/kubernetes.html
* https://github.com/ahmetb/gke-letsencrypt

