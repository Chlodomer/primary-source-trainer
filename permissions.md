# Permissions for Primary Source Trainer Project

**Status**: ✅ ALL PERMISSIONS APPROVED by user on 2025-10-09

## File System Permissions

### Write Permissions
- Create new directories and files in `/Users/yanivfox/Desktop/AI Initiatives/Primary sources/`
- Create project structure (frontend, backend, database folders)
- Write source code files (.js, .jsx, .ts, .tsx, .py, etc.)
- Write configuration files (package.json, tsconfig.json, .env.example, etc.)
- Write documentation files (.md)
- Create asset directories and placeholder files
- Create test files

### Read Permissions
- Read any existing files in the project directory
- Read configuration files to understand setup
- Read source code for editing and debugging

### Edit Permissions
- Modify existing files as needed for development
- Update configuration files
- Refactor code
- Fix bugs

## Command Execution Permissions

### Package Management
- Run `npm init`, `npm install`, `npm update`
- Run `pip install`, `pip freeze`
- Install project dependencies (React, D3, FastAPI/Express, Postgres drivers, etc.)

### Development Server
- Run development servers (`npm run dev`, `npm start`, `uvicorn`, etc.)
- Run build commands (`npm run build`)
- Run test commands (`npm test`, `pytest`)

### Version Control
- Run `git init`, `git add`, `git commit`
- Create branches, merge code
- Run `git push` (when explicitly requested)

### Database
- Run database setup commands
- Run migrations
- Seed database with sample data

### Other Commands
- File operations (mkdir, ls, etc.)
- Process management for dev servers
- Environment setup

## Network Access

### Package Registries
- Access npm registry for JavaScript packages
- Access PyPI for Python packages

### Documentation
- Fetch documentation via WebFetch when needed
- Access GitHub, StackOverflow, official docs

### External Services (Future)
- Email API integration (Postmark/SendGrid) - credentials to be provided later

## Proactive Actions Approved

- Create project scaffolding without asking
- Install standard dependencies
- Write boilerplate code
- Create configuration files
- Set up standard project structure
- Fix errors and bugs autonomously
- Refactor code for best practices
- Write tests

## Actions Requiring Explicit Approval

- Committing to git (must be explicitly requested)
- Pushing to remote repository
- Running destructive commands (rm -rf, DROP TABLE, etc.)
- Modifying git config
- Force operations (--force flags)
- Production deployments
- Sharing credentials or API keys

## Notes

- All permissions are scoped to this project directory
- User email for results sharing: foxyaniv@gmail.com
- Email service credentials will be provided when needed
- Database is Postgres (connection details to be configured)

---

**Reference this document**: Claude can proceed with any approved action without asking again.
