# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e3]:
    - generic [ref=e4]:
      - heading "REFY AI" [level=1] [ref=e5]
      - paragraph [ref=e6]: Plateforme d'analyse immobilière
    - generic [ref=e7]:
      - heading "Connexion" [level=2] [ref=e8]
      - paragraph [ref=e10]: Failed to fetch
      - generic [ref=e11]:
        - generic [ref=e12]:
          - generic [ref=e13]: Email
          - textbox "vous@exemple.com" [ref=e14]: test@refyai.com
        - generic [ref=e15]:
          - generic [ref=e16]: Mot de passe
          - textbox "••••••••" [ref=e17]: password123
        - button "Se connecter" [ref=e18] [cursor=pointer]
      - paragraph [ref=e20]:
        - text: Pas encore de compte ?
        - link "Créer un compte" [ref=e21] [cursor=pointer]:
          - /url: /auth/register
  - alert [ref=e22]
```