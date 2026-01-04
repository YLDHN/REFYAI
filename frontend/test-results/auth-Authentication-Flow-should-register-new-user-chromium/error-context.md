# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e3]:
    - generic [ref=e4]:
      - heading "REFY AI" [level=1] [ref=e5]
      - paragraph [ref=e6]: Plateforme d'analyse immobilière
    - generic [ref=e7]:
      - heading "Créer un compte" [level=2] [ref=e8]
      - paragraph [ref=e10]: Failed to fetch
      - generic [ref=e11]:
        - generic [ref=e12]:
          - generic [ref=e13]: Nom complet (optionnel)
          - textbox "Jean Dupont" [ref=e14]: Test User
        - generic [ref=e15]:
          - generic [ref=e16]: Email
          - textbox "vous@exemple.com" [ref=e17]: test1767197303934@refyai.com
        - generic [ref=e18]:
          - generic [ref=e19]: Mot de passe
          - textbox "••••••••" [ref=e20]: TestPassword123!
          - paragraph [ref=e21]: Minimum 6 caractères
        - button "Créer mon compte" [ref=e22] [cursor=pointer]
      - paragraph [ref=e24]:
        - text: Déjà un compte ?
        - link "Se connecter" [ref=e25] [cursor=pointer]:
          - /url: /auth/login
  - alert [ref=e26]
```